var path = require('path');
var webpack = require('webpack');
var _ = require('lodash')

module.exports = (opts) => {

  const {PROJECT_ROOT, NODE_ENV} = opts;

  var plugins = [
    // add all common plugins here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify(NODE_ENV),
      },
    }),
    // Promise and fetch polyfills
    new webpack.ProvidePlugin({
      Promise: 'imports-loader?this=>global!exports-loader?global.Promise!es6-promise',
      fetch: 'imports-loader?this=>global!exports-loader?global.fetch!whatwg-fetch',
    }),
  ];

  if (NODE_ENV !== 'test') {
    // karma webpack can't use these
    plugins = _.concat(plugins,
      // shared stuff between chuncks
      new webpack.optimize.CommonsChunkPlugin({
        name: 'common',
        minChunks: Infinity,
        filename: 'common.js'
      })
    )
  }

  return {
    context: PROJECT_ROOT,
    output: {
      path: path.resolve(PROJECT_ROOT, 'appserver/static/webpack_bundles/'),
      filename: '[name].js',
    },
    plugins: plugins,
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          loader: 'babel-loader'
        },
        {
          test: /\.scss$/,
          use:[
            'style-loader',
            'css-loader',
            'sass-loader'
          ]
        },
        {
          test: /\.css$/,
          use:[
            'style-loader',
            'css-loader'
          ]
        },
        {
          test: /\.(png|jpg|gif)$/,
          use:[
            {
              loader: "url-loader",
              options: {
                limit: 8192
              }
            }
          ]
        },
        {
          test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
          loader: "file-loader"
        }
      ]
    },
    resolve: {
      extensions: ['.js', '.jsx'],
      modules: [
        path.resolve(PROJECT_ROOT, 'appserver/static/jsx'),
        'node_modules',
      ],
    }
  };
};
