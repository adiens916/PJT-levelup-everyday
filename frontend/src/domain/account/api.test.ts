import {
  checkConnection,
  checkPostAvailability,
  getUserToken,
  login,
  logout,
} from './api';

const USERNAME = 'john';
const PASSWORD = 'johnjohn';

describe.skip('connection tests', () => {
  // If you want to test these, remove '.skip' in 'describe.skip'
  // Ex) describe('connection tests', ... )
  test('check connection', async () => {
    const data = await checkConnection();
    expect(data).toBe('connected');
  });

  test('check post availability', async () => {
    const data = await checkPostAvailability();
    expect(data).toBe('post available');
  });
});

describe.skip('login tests', () => {
  test('login', async () => {
    try {
      const result = await login(USERNAME, PASSWORD);
      expect(result.token).toMatch(/[0-9a-z]{40}/);
      // result.token == c59705415cde035735c37c4711d97f56c49648b6
    } catch (error) {
      console.log(error);
    }
  });

  test('user token should be saved after login', async () => {
    await login(USERNAME, PASSWORD);
    expect(getUserToken()).toMatch(/[0-9a-z]{40}/);
    // result.token == c59705415cde035735c37c4711d97f56c49648b6
  });
});

test('logout', async () => {
  await login(USERNAME, PASSWORD);

  const data = await logout();
  expect(data?.success).toBe(true);
  expect(getUserToken()).toBeNull();
});
