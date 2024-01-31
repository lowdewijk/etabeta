import {useMutation, useQuery, useQueryClient} from 'react-query';
import {toast} from 'react-toastify';

import {
  getEtaBetaState,
  readMessages,
  SendMessage,
  sendMessage,
} from 'src/api_client/session';
import {UserError} from './user_error';

export const useSendMessage = (sessionID: string) => {
  const client = useQueryClient();

  return useMutation(
    (message: SendMessage) => sendMessage(sessionID, message),
    {
      onError: (error: Error) => {
        toast.error('Error sending message: ' + error.message);
      },
      onSuccess: async data => {
        if (data.headers['x-user-error']) {
          const userError = data.data as UserError;
          toast.warning(userError.detail);
        }
        await client.invalidateQueries({queryKey: ['messages']});
      },
    },
  );
};

export const useReadMessages = (sessionID: string, username: string) => {
  // poll for new messages every half second
  return useQuery({
    queryKey: ['readMessages', sessionID, username],
    queryFn: () => readMessages(sessionID, username),
    refetchInterval: 500,
  });
};

export const useGetEtaBetaState = (sessionID: string) => {
  // poll for new messages every half second
  return useQuery({
    queryKey: ['etabeta_messages', sessionID],
    queryFn: () => getEtaBetaState(sessionID),
    refetchInterval: 500,
  });
};
