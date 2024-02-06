module.exports = {
  preset: 'ts-jest/presets/js-with-ts',
  testEnvironment: 'jsdom',
  moduleDirectories: ['src', 'node_modules'],
  rootDir: './',
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/src/__mocks__/fileMock.ts',
    '\\.(css|scss)$': 'identity-obj-proxy',
    'src/(.*)': '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  transformIgnorePatterns: ["/node_modules/(?!(remark-.*|mdast-.*|hast-.*|micromark|decode-named-character-reference|unist-.*|trim-lines|devlop|unified|bail|is-plain-obj|trough|vfile|rehype-.*|comma-separated-token|estree-util-is-identifier-name|property-information|space-separated-tokens))"]
};
