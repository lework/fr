import axios from '@utils/request';

export function login (user) {
    const url = '/login/';
    return axios.post(url,
        user
    ).then((res) => {
        return Promise.resolve(res.data);
    });
}

export function logout () {
  const url = '/login/';
  return axios.delete(url).then((res) => {
      return Promise.resolve(res.data);
  });
}