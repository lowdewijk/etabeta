import { Configuration as WebpackConfiguration } from "webpack";
import { Configuration as WebpackDevServerConfiguration } from "webpack-dev-server";
import {merge} from "webpack-merge";

import {outDir} from './build-constants.js';
import commonConfig from './webpack.common.config.js';

interface Configuration extends WebpackConfiguration {
  devServer?: WebpackDevServerConfiguration;
}

const devSpecificConfig: Configuration = {
  mode: "development",
  output: {
    publicPath: "/",
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  devtool: "inline-source-map",
  devServer: {
    static: {
      directory: outDir,
    },
    historyApiFallback: true,
    port: 4000,
    open: true,
    hot: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
};

const config: Configuration = merge(commonConfig, devSpecificConfig);

export default config;
