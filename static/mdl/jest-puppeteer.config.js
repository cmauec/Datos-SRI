module.exports = {
  launch: {
    headless: process.env.HEADLESS !== 'false', // Run in headless mode by default
    // slowMo: process.env.SLOWMO ? process.env.SLOWMO : 0, // Useful for debugging
    // args: ['--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox'] // Common args for CI environments
  },
  browserContext: 'default', // Can be 'incognito'
};
