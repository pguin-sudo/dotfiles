return {
  'iamcco/markdown-preview.nvim',
  build = 'cd app && bun install',
  config = function()
    vim.g.mkdp_filetypes = { 'markdown' }
  end,
  ft = { 'markdown' },
  cmd = { 'MarkdownPreviewToggle', 'MarkdownPreview', 'MarkdownPreviewStop' },
}
