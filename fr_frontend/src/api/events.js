import axios from '@utils/request';


export function getEventList (search, page, pageSize) {
  let url = '/accidents/event/';
  if (search) {
      url += '?search=' + search;
      url += page ? '&page=' + page : '&page=' + 1;
  } else {
      url += page ? '?page=' + page : '?page=' + 1;
  }
  if (pageSize) {
      url += '&size=' + pageSize;
  }
  return axios.get(url).then((res) => {
      return Promise.resolve(res.data);
  });
}

export function getEventDetail (id) {
  let url = '/accidents/event/' + id;
  return axios.get(url).then((res) => {
      return Promise.resolve(res.data);
  });
}


export function editEventDetail (data) {
  let url = `/accidents/event/${data.id}/`;
  return axios.patch(url, data).then((res) => {
      return Promise.resolve(res.data);
  });
}

export function addEvent (data) {
  let url = '/accidents/event/'
  return axios.post(url, data).then((res) => {
      return Promise.resolve(res.data);
  });
}

export function deleteEvent (id) {
  let url = '/accidents/event/' + id;
  return axios.delete(url).then((res) => {
      return Promise.resolve(res.data);
  });
}



export function editRecordDetail (data) {
  let url = `/accidents/record/${data.id}/`;
  return axios.patch(url, data).then((res) => {
      return Promise.resolve(res.data);
  });
}

export function addRecord (data) {
  let url = '/accidents/record/'
  return axios.post(url, data).then((res) => {
      return Promise.resolve(res.data);
  });
}