if arg[2] < 2 then
  goto postfinished
end

local sysconfdir = rpm.expand('%{_sysconfdir}')
local provider_fips = sysconfdir .. "/ssl/provider_fips.cnf"
local provider_base = sysconfdir .. "/ssl/provider_base.cnf"
local default_provider = sysconfdir .. "/ssl/provider_default.cnf"
local distro_cnf = sysconfdir .. "/ssl/distro.cnf"

local st = posix.stat(provider_fips)
if not st or st.size <= 0 then
  goto postfinished
end

-- Function to (un)comment a line
function comment(provider, prefix)
  local pattern = "#?(%.include " .. provider .. ")"
  local f = io.open(distro_cnf, "r")
  if not f then
    error("Failed to open " .. distro_cnf)
  end

  local content = f:read("*all")
  f:close()

  local new_content, count = content:gsub(pattern, prefix .. "%1")

  -- count > 0 means we found a match, but it's possible nothing changed,
  -- so check for that too.
  if count == 0 or content == new_content then
    return 0
  end

  local f = io.open(distro_cnf, "w")
  if not f then
    error("Failed to reopen " .. distro_cnf .. " for writing!")
    return 0
  end

  f:write(new_content)
  f:close()

  return 1
end

-- Uncomment FIPS provider
if comment(provider_fips, "") == 0 then
  -- If already uncommented, let's just skip out early
  goto postfinished
end

-- Unomment base provider
comment(provider_base, "")

-- Comment default provider
comment(default_provider, "#")

::postfinished::
