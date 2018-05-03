const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,

  entry: {
    search: "./gdpr/static/js/Search"
  },

  output: {
    path: path.resolve("./gdpr/static/bundles/"),
    filename: "[name]-[hash].js"
  },

  plugins: [new BundleTracker({ filename: "./webpack-stats.json" })],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: "babel-loader",
        exclude: /node_modules/,
        query: {
          presets: ["es2015", "react"]
        }
      }
    ]
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".jsx"]
  }
};
