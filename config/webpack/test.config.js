var path = require('path');
var baseConfig = require('./base.config.js')
var _ = require('lodash')

module.exports = (opts) => {

  const config = baseConfig(opts);
  var {PROJECT_ROOT, CDN_PATH} = opts;
  const plugins =  config.plugins;
  const modules = _.assign(config.module, {
    rules: _.concat(config.module.rules, {
        test: /(\.jsx|\.js)$/, loader: 'eslint-loader', exclude: /node_modules/
      }
    )
  })
  return _.assign(config, {
    devtool: 'inline-source-map',
    plugins: plugins
  })
};
