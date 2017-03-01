var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var baseConfig = require('./base.config.js')
var _ = require('lodash')

module.exports = (opts) => {

  const config = baseConfig(opts);
  var {PROJECT_ROOT, CDN_PATH} = opts;
  const plugins =  _.concat(config.plugins,
    // local bundle stats file
    new BundleTracker({filename: './webpack-stats.json'}),
    new CopyWebpackPlugin([
      {
        from: path.resolve(PROJECT_ROOT, 'capricorn/static/admin-lte'),
        to: path.resolve(PROJECT_ROOT, 'capricorn/static/dist/admin-lte')
      }
    ]),
    new CaseSensitivePathsPlugin(),  // OSX wont check but other unix os will
    new webpack.NoEmitOnErrorsPlugin(),
      // minifies your code
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
      output: {
        comments: false,
      },
      sourceMap: false,
    })
  )

  const output = _.assign(
    config.output,
    {
        path: path.resolve(PROJECT_ROOT, 'capricorn/static/dist/'),
        publicPath: CDN_PATH || '/static/webpack_bundles/',
    }
  )

  return _.assign(config, {
    output: output,
    entry: {
      'delivery-tools': path.resolve(PROJECT_ROOT, 'capricorn/static/jsx/frontend-app'),
      // vendor: ['react', 'redux', 'react-router', 'react-redux', 'react-dom'],
    },
    plugins: plugins
  })
};
