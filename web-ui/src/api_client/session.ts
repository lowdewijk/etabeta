import axios from 'axios';

export type SendMessage = {
  message: string;
  username: string;
};

export type Message = {
  message: string;
  username: string;
  timestamp: number;
};

export type GetMessages = {
  sessionID: string;
  messages: Array<Message>;
};

export const sendMessage = async (sessionID: string, message: SendMessage) => {
  return axios.post(
    `http://localhost:8000/api/session/${sessionID}/send_message`,
    message,
  );
};

export const getMessages = async (
  sessionID: string,
): Promise<Array<Message>> => {
  const response = await axios.get<GetMessages>(
    `http://localhost:8000/api/session/${sessionID}/messages`,
  );
  return response.data.messages;
};

export const getEtaBetaMessages = async (
  sessionID: string,
): Promise<Array<Message>> => {
  const response = await axios.get<GetMessages>(
    `http://localhost:8000/api/session/${sessionID}/etabeta_messages`,
  );
  return response.data.messages;
};
