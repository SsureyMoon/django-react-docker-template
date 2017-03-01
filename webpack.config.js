const OPTIONS = {
  PROJECT_ROOT: process.env.PROJECT_ROOT || __dirname,
  NODE_ENV: process.env.NODE_ENV,
  CDN_PATH: process.env.CDN_PATH,
};


module.exports = (function() {
  switch (process.env.NODE_ENV) {
    case 'local':
      return require('./config/webpack/local.config.js');
    case 'develop':
      return require('./config/webpack/develop.config.js');
    case 'staging':
      return require('./config/webpack/staging.config.js');
    case 'production':
      return require('./config/webpack/production.config.js');
    case 'test':
      return require('./config/webpack/test.config.js');
    default:
      return require('./config/webpack/local.config.js');
  }
})()(OPTIONS);
