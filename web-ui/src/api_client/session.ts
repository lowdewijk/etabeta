import axios from 'axios';

export type Message = {
  message: string;
  username: string;
};

export const sendMessage = async (sessionID: string, message: Message) => {
  return axios.post(
    `http://localhost:8000/api/session/${sessionID}/send_message`,
    message,
  );
};

type GetMessages = {
  sessionID: string;
  messages: Array<Message>;
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
    `http://localhost:8000/api/session/${sessionID}/eta_beta_messages`,
  );
  return response.data.messages;
};
