var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var baseConfig = require('./base.config.js')
var _ = require('lodash')

module.exports = (opts) => {

  const config = baseConfig(opts);
  const {PROJECT_ROOT} = opts;
  const devServer = {
    contentBase: path.resolve(PROJECT_ROOT, 'capricorn/static/jsx'),
    host: "0.0.0.0",
    port: 8080,
    hot: true,
    watchContentBase: true,
    publicPath: 'http://localhost:8080/static/webpack_bundles/'
  }

  const plugins =  _.concat(config.plugins,
    // local bundle stats file
    new BundleTracker({filename: './webpack-stats.json'}),
    new CaseSensitivePathsPlugin(),  // OSX wont check but other unix os will
    new webpack.NoEmitOnErrorsPlugin()
  )

  const output = _.assign(
    config.output,
    { publicPath: 'http://localhost:8080/static/webpack_bundles/'}
  )

  return _.assign(config, {
    output: output,
    entry: {
      'frontend-app': path.resolve(PROJECT_ROOT, 'capricorn/static/jsx/frontend-app'),
    },
    plugins: plugins,
  })
};
