/** @type {import('jest').Config} */
const config = {
  preset: 'jest-puppeteer',
  testMatch: ['**/test/**/*.test.js'], // Assuming tests will be in a 'test' subdirectory and end with .test.js
  setupFilesAfterEnv: ['./jest.setup.js'], // Optional: for global setup/teardown for tests
};

module.exports = config;
