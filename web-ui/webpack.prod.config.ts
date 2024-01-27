import webpack from "webpack";
import merge from "webpack-merge";
import MiniCssExtractPlugin from "mini-css-extract-plugin";

import commonConfig from './webpack.common.config';

const prodSpecificConfig: webpack.Configuration = {
  mode: "production",
  output: {
    filename: "[name].[contenthash].js",
    publicPath: "",
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].[contenthash].css",
    }),
  ],
};

const config: webpack.Configuration = merge(commonConfig, prodSpecificConfig);

export default config;
