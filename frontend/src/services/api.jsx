import axios from 'axios';

const API = axios.create({ 
    baseURL: 'http://localhost:5000'
});

export const scanCard = async (imageData: FormData) => {
    return API.post('/api/scan', imageData);
};
