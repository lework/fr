import Cookies from 'js-cookie';

const USERKEY = 'user';
const TOKENKEY = 'Token';
const CSRFKEY = 'csrftoken';

export function loadUser () {
    const value = Cookies.get(USERKEY);
    return value || '';
}

export function loadToken () {
    const value = Cookies.get(TOKENKEY);
    return value || '';
}

export function loadCsrfToken () {
    const value = Cookies.get(CSRFKEY);
    return value || '';
}

export function saveLoginInfo (info) {
    Cookies.set(USERKEY, info.username, {expires: new Date(info.expires) });
    Cookies.set(TOKENKEY, info.token, {expires: new Date(info.expires) });
}

export function removeLoginInfo () {
    Cookies.remove(USERKEY);
    Cookies.remove(TOKENKEY);
}
