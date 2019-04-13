const path = require('path');
const htmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin'); //15版本之后需要配置这项
const webpack = require('webpack');

module.exports = {
    entry: './src/main.js',
    output: {
	path: path.resolve(__dirname, './dist'),
	filename: 'bundle.js'
    },
    plugins: [
	new htmlWebpackPlugin({
	    template: './public/index.html',
	    filename: 'index.html'
	}),
	new VueLoaderPlugin(),
    ],
    module: {
    	rules: [
    	    { test: /\.css$/, use: ['style-loader', 'css-loader'] },
    	    { test: /\.less$/, use: ['style-loader', 'css-loader', 'less-loader'] },
    	    { test: /\.(jpg|png|gif|bmp|jpeg)$/, use: 'url-loader?limit=12000&name=[hash:12]-[name]-[ext]' },
    	    { test: /\.(ttf|eot|svg|woff|woff2)$/, use: 'url-loader' },
    	    { test: /\.js$/, use: 'babel-loader', exclude: /node_modules/ },
	    { test: /\.vue$/, use: 'vue-loader' },
    	]
    },
    resolve: {
	alias: {
	    'vue$': 'vue/dist/vue.js',
	}
    },
};
