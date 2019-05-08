const { addLessLoader, override } = require("customize-cra");

const loaderOptions = {
  javascriptEnabled: true,
  localIdentName: '[local]--[hash:base64:5]',
  noIeCompat: true,
  strictMath: true
};

module.exports = override(addLessLoader(loaderOptions));
