const webpack = require('webpack')

module.exports = {
    devServer: {
        proxy: {
            '^/api': {
                target: 'http://localhost:8080',
                ws: true,
                changeOrigin: true
            }
        }
    },
    configureWebpack: config => {
        return {
            plugins: [
                new webpack.DefinePlugin({
                    '__FRONTEND_VERSION__': JSON.stringify(require('./package.json').version),
                })
            ]
        }
    },
}