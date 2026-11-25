-- Presentation only: the source Markdown supplies every project and achievement.
local stringify = pandoc.utils.stringify
local korean = false
local section_names = {
  ['어학 능력'] = 'Language Skills',
  ['학력'] = 'Education',
  ['기술 역량'] = 'Technical Skills',
  ['프로젝트'] = 'Projects',
  ['병역'] = 'Military Service',
}

local function raw(value)
  return pandoc.RawBlock('latex', value)
end

local function tex(inlines)
  return pandoc.write(pandoc.Pandoc({pandoc.Plain(inlines)}), 'latex'):gsub('%s+$', '')
end

local function text(value)
  return tex({pandoc.Str(value)})
end

local function lines(inlines, include_softbreaks)
  local result, line = {}, pandoc.List()
  for _, inline in ipairs(inlines) do
    if inline.t == 'LineBreak' or (include_softbreaks and inline.t == 'SoftBreak') then
      result[#result + 1] = line
      line = pandoc.List()
    else
      line:insert(inline)
    end
  end
  result[#result + 1] = line
  return result
end

local function unitalic(inlines)
  if #inlines == 1 and inlines[1].t == 'Emph' then
    return inlines[1].content
  end
  return inlines
end

local function links_only(block)
  if block.t ~= 'Para' then return false end
  for _, inline in ipairs(block.content) do
    if inline.t ~= 'Link' and inline.t ~= 'SoftBreak' and inline.t ~= 'Space' then
      return false
    end
  end
  return true
end

local function link_line(block)
  local result = {}
  for _, inline in ipairs(block.content) do
    if inline.t == 'Link' then
      local url, label = inline.target, stringify(inline.content)
      if url:match('^https://github%.com/') then
        if url:match('%-commit%-analysis/?$') then label = korean and '분석' or 'Analysis'
        elseif url:match('%-results/?$') then label = korean and '결과' or 'Results'
        elseif url:match('%-web/?$') then label = korean and '웹' or 'Web'
        else label = 'GitHub' end
      elseif url:match('^https://play%.google%.com/') then label = 'Google Play'
      elseif url:match('^https://apps%.apple%.com/') then label = 'App Store'
      end
      result[#result + 1] = tex({pandoc.Link({pandoc.Str(label)}, url, inline.title)})
    end
  end
  return table.concat(result, ' \\enspace\\textperiodcentered\\enspace ')
end

local function project_heading(title, date, links)
  local name, description = title:match('^(.-):%s*(.+)$')
  if not name then name, description = title:match('^(.-)%s+—%s+(.+)$') end
  return '\\cvproject{' .. text(name or title) .. '}{' .. text(description or '') .. '}{' .. text(date or '') .. '}{' .. (links or '') .. '}'
end

local function role_lines(block, links, title)
  local parts = lines(block.content)
  local role, date = stringify(unitalic(parts[1])):match('^(.-)%s+|%s+(.+)$')
  local stack = {}
  for i = 2, #parts do stack[#stack + 1] = tex(unitalic(parts[i])) end
  local result = {
    project_heading(title, date and date:gsub(' %- ', ' – ') or '', links),
    '\\cvdetails{' .. (role and text(role) or tex(unitalic(parts[1]))) .. '}{' .. table.concat(stack, '; ') .. '}'
  }
  return raw(table.concat(result, '\n'))
end

function Pandoc(doc)
  korean = stringify(doc.meta.lang or '') == 'ko'
  local output, section = pandoc.List(), nil
  local entry_open = false
  local pending_links = nil
  local pending_title = nil

  local function flush_title()
    if pending_title then
      output:insert(raw(project_heading(pending_title)))
      pending_title = nil
    end
  end

  local function flush_links()
    if pending_links then
      output:insert(raw('\\cvlinks{' .. pending_links .. '}'))
      pending_links = nil
    end
  end

  local function close_entry()
    flush_title()
    flush_links()
    if entry_open then
      output:insert(raw('\\end{cventry}'))
      entry_open = false
    end
  end

  for _, block in ipairs(doc.blocks) do
    if block.t == 'Header' then
      close_entry()
      local title = stringify(block.content):gsub('^%d+[%d%-]*%.%s*', '')
      if block.level == 1 then
        output:insert(raw('\\cvname{' .. tex(block.content) .. '}'))
        section = 'contact'
      elseif block.level == 2 then
        local display_section = stringify(block.content)
        section = section_names[display_section] or display_section
        if section ~= 'Language Skills' and section ~= 'Projects' then
          output:insert(raw('\\cvsection{' .. text(korean and display_section or section) .. '}'))
        end
      elseif block.level == 3 then
        output:insert(raw('\\cvsection{' .. text(title) .. '}'))
      else
        output:insert(raw('\\begin{cventry}'))
        pending_title = title
        entry_open = true
      end
    elseif section == 'contact' and block.t == 'BulletList' then
      local contacts = {}
      for _, item in ipairs(block.content) do
        local value = stringify(item):gsub('^[^:]+:%s*', '')
        if value:find('@', 1, true) then
          contacts[#contacts + 1] = '\\href{mailto:' .. value .. '}{' .. text(value) .. '}'
        else
          local link = nil
          for _, inline in ipairs(item[1].content) do
            if inline.t == 'Link' then link = inline end
          end
          contacts[#contacts + 1] = link and tex({link}) or text(value)
        end
      end
      output:insert(raw('\\cvcontact{' .. table.concat(contacts, ' \\enspace\\textperiodcentered\\enspace ') .. '}'))
    elseif section == 'Language Skills' and block.t == 'BulletList' then
      local values = {}
      for _, item in ipairs(block.content) do
        local value = tex(item[1].content)
        if item[2] and item[2].t == 'BulletList' then
          value = value .. ' \\enspace— ' .. text(stringify(item[2]))
        end
        values[#values + 1] = value
      end
      output:insert(raw('\\cvcontact{' .. table.concat(values, ' \\qquad ') .. '}'))
    elseif section == 'Technical Skills' and block.t == 'Para' then
      local rows = {}
      for _, line in ipairs(lines(block.content, true)) do
        if line[1] and line[1].t == 'Strong' then
          local label = line:remove(1)
          if line[1] and line[1].t == 'Str' and line[1].text == ':' then line:remove(1) end
          if line[1] and line[1].t == 'Space' then line:remove(1) end
          rows[#rows + 1] = tex({label}) .. ' & ' .. tex(line) .. ' \\\\'
        else
          rows[#rows + 1] = '\\multicolumn{2}{@{}l@{}}{' .. tex(line) .. '} \\\\'
        end
      end
      output:insert(raw('\\begin{cvskills}\n' .. table.concat(rows, '\n') .. '\n\\end{cvskills}'))
    elseif (section == 'Education' or section == 'Military Service') and block.t == 'Para' then
      local parts = lines(block.content)
      local date_index
      for i, line in ipairs(parts) do
        if #line == 1 and line[1].t == 'Emph' then date_index = i end
      end
      if date_index then
        output:insert(raw('\\cvrow{' .. tex(parts[1]) .. '}{\\cvdate{' .. tex(unitalic(parts[date_index])) .. '}}'))
        if section == 'Education' and parts[4] then
          output:insert(raw('\\cvrow{' .. tex(parts[2]) .. '}{' .. tex(parts[4]) .. '}'))
        else
          output:insert(pandoc.Para(parts[2]))
        end
      else
        output:insert(block)
      end
    elseif entry_open and links_only(block) then
      pending_links = link_line(block)
    elseif entry_open and block.t == 'Para' and block.content[1].t == 'Emph' then
      output:insert(role_lines(block, pending_links, pending_title))
      pending_title = nil
      pending_links = nil
    elseif entry_open and block.t == 'Para' and #block.content == 1 and block.content[1].t == 'Strong' then
      flush_links()
      output:insert(raw('\\cvaward{' .. tex(block.content[1].content) .. '}'))
    else
      flush_title()
      flush_links()
      output:insert(block)
    end
  end
  close_entry()
  doc.blocks = output
  return doc
end
