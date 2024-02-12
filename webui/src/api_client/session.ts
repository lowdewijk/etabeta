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

export const joinSession = async (sessionID: string, username: string) => {
  return axios.post(`/api/session/${sessionID}/join/${username}`);
};

export const leaveSession = async (sessionID: string, username: string) => {
  return axios.post(`/api/session/${sessionID}/leave/${username}`);
};

export const sendMessage = async (sessionID: string, message: SendMessage) => {
  return axios.post(`/api/session/${sessionID}/send_message`, message);
};

export const readMessages = async (
  sessionID: string,
  username: string,
): Promise<Array<Message>> => {
  const response = await axios.get<GetMessages>(
    `/api/session/${sessionID}/messages/${username}`,
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
