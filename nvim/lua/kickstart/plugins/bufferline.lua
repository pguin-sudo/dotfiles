-- bufferline


return {
    'akinsho/bufferline.nvim',
    version = '*',
    dependencies = { 
        'nvim-tree/nvim-web-devicons',
    },
    config = function()
        require('bufferline').setup {
            options = {
                mode = "buffers",
                themable = true,
                color_icons = true,
                offsets = {
                    {
                        filetype = "neo-tree",
                        text = "File Explorer",
                        text_align = "left",
                        separator = true,
                    }
                },
            }
        }

        -- Keymaps for bufferline
        vim.keymap.set('n', '<A-h>', '<cmd>BufferLineCyclePrev<CR>', { silent = true })
        vim.keymap.set('n', '<A-l>', '<cmd>BufferLineCycleNext<CR>', { silent = true })
        vim.keymap.set('n', '<A-k>', '<cmd>BufferLineCloseOthers<CR>', { silent = true })
    end,
}

