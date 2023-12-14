import axios from 'axios';

export const createSession = async (sessionID: string) => {
  return axios.post('http://localhost:8000/api/session', {sessionID});
};

export const deleteSession = async (sessionID: string) => {
  return axios.delete(`http://localhost:8000/api/session/${sessionID}`);
};

export type Message = {
  message: string;
  username: string;
};

export const sendMessage = async (sessionID: string, message: Message) => {
  return axios.post(
    `http://localhost:8000/api/session/${sessionID}/message`,
    message,
  );
};

type GetMessages = {
  sessionID: string;
  messages: Message[];
};

export const getMessages = async (sessionID: string) => {
  const response = await axios.get<GetMessages>(
    `http://localhost:8000/api/session/${sessionID}/messages`,
  );
  return response.data.messages;
};
