/**
 * @jest-environment node
 */

import { login } from './api';

const USERNAME = 'john';
const PASSWORD = 'johnjohn';

test('login', async () => {
  /* TODO: It says a token is needed but login doesn't need any token exceptionally */
  const result = await login(USERNAME, PASSWORD);

  // result.token == c59705415cde035735c37c4711d97f56c49648b6
  expect(result.token).toHaveLength(40);
  expect(result.token).toMatch(/[0-9a-z]{40}/);
});
