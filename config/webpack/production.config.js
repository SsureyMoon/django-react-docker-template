var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var baseConfig = require('./base.config.js')
var _ = require('lodash')

module.exports = (opts) => {

  const config = baseConfig(opts);
  const {PROJECT_ROOT, CDN_PATH} = opts;

  const plugins =  _.concat(config.plugins,
    // local bundle stats file
    new CopyWebpackPlugin([]),
    new CaseSensitivePathsPlugin(),  // OSX wont check but other unix os will
    new webpack.NoErrorsPlugin(),
    // minifies your code
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
      output: {
        comments: false,
      },
      sourceMap: false,
    }),
      // removes duplicate modules
      new webpack.optimize.DedupePlugin()
  )

  const output = _.assign(
    config.output,
    {
        path: path.resolve(PROJECT_ROOT, 'appserver/static/dist/'),
        publicPath: CDN_PATH || '/static/webpack_bundles/'
    }
  )

  return _.assign(config, {
    output: output,
    entry: {
      'frontend-app': path.resolve(PROJECT_ROOT, 'appserver/static/jsx/frontend-app')
    },
    plugins: plugins
  })
};
