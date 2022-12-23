const host = 'http://localhost:62221';
const resource = 'habits';

export async function getHabits() {
  return await request(`${host}/${resource}`);
}

async function request(url: string) {
  try {
    const response = await fetch(url);
    if (response.ok) {
      return response.json();
    } else {
      console.log('Response not okay: ', response);
    }
  } catch (error) {
    console.log('Server error: ', error);
  }
}
