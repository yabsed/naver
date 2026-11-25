-- Presentation only: build.py supplies every entry, date and image; this maps them to template macros.
local function raw(value)
  return pandoc.RawBlock('latex', value)
end

local function tex(inlines)
  local doc = pandoc.Pandoc({pandoc.Plain(inlines)})
  local out = pandoc.write(doc, 'latex', pandoc.WriterOptions({wrap_text = 'wrap-none'}))
  return (out:gsub('%s+$', ''))
end

-- Korean text takes quotes, parentheses and ellipses from the Hangul face (see \koreantext).
local function language(element)
  local hangul, letters = 0, 0
  for _, code in utf8.codes(pandoc.utils.stringify(element.content)) do
    if code >= 0xAC00 and code <= 0xD7A3 then hangul = hangul + 1 end
    if code > 0x40 then letters = letters + 1 end
  end
  if hangul * 2 > letters then
    -- No TeX group here: a group opened before the paragraph starts would undo wrapfig's line shape.
    element.content:insert(1, pandoc.RawInline('latex', '\\koreantext{}'))
    element.content:insert(pandoc.RawInline('latex', '\\latintext{}'))
  end
  return element
end
Para, Plain, Header = language, language, language

-- Fixed-width blocks: keep line breaks and leading spaces; Symbola covers glyphs D2Coding lacks.
local function panel(block)
  local rows = {}
  for line in (block.text .. '\n'):gmatch('(.-)\n') do
    local indent, rest = line:match('^( *)(.*)$')
    if rest == '' then
      rows[#rows + 1] = '\\mbox{}'
    else
      local value = tex({pandoc.Str(rest)}):gsub('🔒', '{\\symfont 🔒}')
      if #indent > 0 then value = '\\hspace*{' .. (#indent * 0.5) .. 'em}' .. value end
      rows[#rows + 1] = value
    end
  end
  return raw('\\begin{panel}\n' .. table.concat(rows, '\\\\\n') .. '\n\\end{panel}')
end

local inner = {
  CodeBlock = panel,
  Div = function(block)
    if not block.classes:includes('links') then return nil end
    local out = pandoc.List()
    for _, list in ipairs(block.content) do
      for _, item in ipairs(list.t == 'BulletList' and list.content or {}) do
        out:insert(raw('\\linkline{' .. tex(pandoc.utils.blocks_to_inlines(item)) .. '}'))
      end
    end
    return out
  end,
  BlockQuote = function(block)
    local out = pandoc.List({raw('\\begin{notequote}')})
    out:extend(block.content)
    out:insert(raw('\\end{notequote}'))
    return out
  end,
  Header = function(block)
    local macro = block.level <= 3 and '\\innerheadA' or '\\innerheadB'
    return raw(macro .. '{' .. tex(block.content) .. '}')
  end,
}

local function entry(div)
  local a = div.attributes
  local blocks = pandoc.List(div.content)
  local title, deck
  if blocks[1] and blocks[1].t == 'Header' and blocks[1].level == 2 then
    title = tex(blocks:remove(1).content)
  end
  if blocks[1] and blocks[1].t == 'Div' and blocks[1].classes:includes('deck') then
    deck = tex(blocks:remove(1).content[1].content)
  end
  local body = pandoc.walk_block(pandoc.Div(blocks), inner).content

  local out = pandoc.List({raw('\\entrystart{' .. a.need .. 'mm}')})
  if title then
    local macro = a.kind == 'headline' and '\\headlinehead' or '\\notehead'
    out:insert(raw(macro .. '{' .. title .. '}{' .. a.date .. '}'))
  else
    out:insert(raw('\\datehead{' .. a.date .. '}'))
  end
  if deck then out:insert(raw('\\entrydeck{' .. deck .. '}')) end
  if a.mode == 'columns' then
    out:insert(raw('\\begin{multicols}{2}'))
    if a.img then out:insert(raw('\\columnimage{' .. a.img .. '}')) end
    out:extend(body)
    out:insert(raw('\\end{multicols}'))
  elseif a.img and a.mode == 'side' then
    out:insert(raw('\\begin{sideimage}{' .. a.img .. '}{' .. a.imgw .. 'mm}'))
    out:extend(body)
    out:insert(raw('\\end{sideimage}'))
  else
    -- A date that opens the body sits directly under the head row, above any image.
    if body[1] and body[1].t == 'RawBlock' and body[1].text:match('^\\piecedate') then
      out:insert(raw((body:remove(1).text:gsub('^\\piecedate', '\\firstpiecedate'))))
    end
    if a.img then out:insert(raw('\\leadimage{' .. a.img .. '}{' .. a.imgw .. 'mm}')) end
    out:extend(body)
  end
  out:insert(raw('\\entryfinish'))
  return out
end

function Pandoc(doc)
  local output = pandoc.List()
  for _, block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level == 1 then
      output:insert(raw('\\cvsection{' .. tex(block.content) .. '}'))
    elseif block.t == 'Div' and block.classes:includes('entry') then
      output:extend(entry(block))
    else
      output:insert(block)
    end
  end
  doc.blocks = output
  return doc
end
