import axios from 'axios';

const client = axios.create({
    baseURL: 'http://localhost:8000/api'
    // Other configurations if needed
});

export default client;
