import {useMutation, useQuery, useQueryClient} from 'react-query';
import {toast} from 'react-toastify';

import {
  getEtaBetaMessages,
  getMessages,
  Message,
  sendMessage,
} from 'src/api_client/session';

export const useSendMessage = (sessionID: string) => {
  const client = useQueryClient();

  return useMutation((message: Message) => sendMessage(sessionID, message), {
    onError: (error: Error) => {
      toast.error('Error sending message: ' + error.message);
    },
    onSuccess: async () => {
      await client.invalidateQueries({queryKey: ['messages']});
    },
  });
};

export const useGetMessages = (sessionID: string) => {
  // poll for new messages every half second
  return useQuery({
    queryKey: ['messages', sessionID],
    queryFn: () => getMessages(sessionID),
    refetchInterval: 500,
  });
};

export const useGetEtaBetaMessages = (sessionID: string) => {
  // poll for new messages every half second
  return useQuery({
    queryKey: ['messages', sessionID],
    queryFn: () => getEtaBetaMessages(sessionID),
    refetchInterval: 500,
  });
};
