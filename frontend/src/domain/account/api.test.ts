import { checkConnection, checkPostAvailability, login } from './api';

test('login', async () => {
  try {
    const result = await login('john', 'johnjohn');
    expect(result.token).toMatch(/[0-9a-z]{40}/);
    // result.token == c59705415cde035735c37c4711d97f56c49648b6
  } catch (error) {
    console.log(error);
  }
});

test('check connection', async () => {
  const data = await checkConnection();
  expect(data).toBe('connected');
});

test('check post availability', async () => {
  const data = await checkPostAvailability();
  expect(data).toBe('post available');
});
