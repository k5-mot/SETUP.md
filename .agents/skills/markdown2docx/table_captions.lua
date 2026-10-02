local function caption_inlines(block)
  if block.t ~= "Para" or #block.content == 0 then
    return nil
  end
  local first = block.content[1]
  if first.t ~= "Str" then
    return nil
  end
  local marker = string.lower(first.text)
  if marker ~= ":" and marker ~= "table:" then
    return nil
  end
  local content = {}
  for index = 2, #block.content do
    if not (index == 2 and block.content[index].t == "Space") then
      table.insert(content, block.content[index])
    end
  end
  if pandoc.utils.stringify(content) == "" then
    return nil
  end
  return content
end

local function numbered_caption(number, content)
  local inlines = { pandoc.Str("表 " .. number .. ": ") }
  for _, inline in ipairs(content) do
    table.insert(inlines, inline)
  end
  return pandoc.Caption({ pandoc.Plain(inlines) }, {})
end

function Pandoc(document)
  local blocks = {}
  local heading = "表"
  local heading_counts = {}
  local table_number = 0
  local index = 1

  while index <= #document.blocks do
    local block = document.blocks[index]
    if block.t == "Header" then
      heading = pandoc.utils.stringify(block.content)
      table.insert(blocks, block)
    elseif block.t == "Para"
      and index < #document.blocks
      and document.blocks[index + 1].t == "Table"
      and caption_inlines(block) then
      table_number = table_number + 1
      local table_block = document.blocks[index + 1]
      table_block.caption = numbered_caption(table_number, caption_inlines(block))
      table.insert(blocks, table_block)
      index = index + 1
    elseif block.t == "Table" then
      local content = nil
      if index < #document.blocks then
        content = caption_inlines(document.blocks[index + 1])
        if content then
          index = index + 1
        end
      end
      if not content then
        heading_counts[heading] = (heading_counts[heading] or 0) + 1
        local occurrence = heading_counts[heading]
        local title = heading
        if occurrence > 1 then
          title = title .. "（" .. occurrence .. "）"
        end
        content = { pandoc.Str(title) }
      end
      table_number = table_number + 1
      block.caption = numbered_caption(table_number, content)
      table.insert(blocks, block)
    else
      table.insert(blocks, block)
    end
    index = index + 1
  end

  document.blocks = blocks
  return document
end
