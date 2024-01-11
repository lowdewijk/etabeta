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

export type EtaBetaArgument = {
  argument: string;
  counter_arguments: Array<EtaBetaArgument>;
};

export type EtaBetaState = {
  scores: {[user: string]: number};
  messages: Array<Message>;
  in_court?: string;
  summary?: Array<EtaBetaArgument>;
  under_observation: Array<number>;
};

export const sendMessage = async (sessionID: string, message: SendMessage) => {
  return axios.post(`/api/session/${sessionID}/send_message`, message);
};

export const getMessages = async (
  sessionID: string,
): Promise<Array<Message>> => {
  const response = await axios.get<GetMessages>(
    `/api/session/${sessionID}/messages`,
  );
  return response.data.messages;
};

export const getEtaBetaState = async (
  sessionID: string,
): Promise<EtaBetaState> => {
  const response = await axios.get<EtaBetaState>(
    `/api/session/${sessionID}/etabeta_messages`,
  );
  return response.data;
};
