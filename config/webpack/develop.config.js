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
        from: path.resolve(PROJECT_ROOT, 'appserver/static/admin-lte'),
        to: path.resolve(PROJECT_ROOT, 'appserver/static/dist/admin-lte')
      }
    ]),
    new CaseSensitivePathsPlugin(),  // OSX wont check but other unix os will
    new webpack.NoEmitOnErrorsPlugin()
  )

  const output = _.assign(
    config.output,
    {
        path: path.resolve(PROJECT_ROOT, 'appserver/static/dist/'),
        publicPath: CDN_PATH || '/static/webpack_bundles/',
    }
  )

  return _.assign(config, {
    output: output,
    entry: {
      'frontend-app': path.resolve(PROJECT_ROOT, 'appserver/static/jsx/frontend-app'),
    },
    plugins: plugins
  })
};
