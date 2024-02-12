import {useMutation, useQuery, useQueryClient} from 'react-query';
import {toast} from 'react-toastify';

import {
  getEtaBetaState,
  joinSession,
  leaveSession,
  readMessages,
  SendMessage,
  sendMessage,
} from '../api_client/session';
import {UserError} from './user_error';

const onError = (operation: string) => {
  return {
    onError: (error: Error) => {
      toast.error(`Error during ${operation}: ${error.message}`);
    },
  };
};

export const useJoinSession = () => {
  return useMutation(
    ({sessionID, username}: {sessionID: string; username: string}) =>
      joinSession(sessionID, username),
    {
      ...onError('joining session'),
      onSuccess: () => console.log(`Joined session`),
    },
  );
};

export const useLeaveSession = () => {
  return useMutation(
    ({sessionID, username}: {sessionID: string; username: string}) =>
      leaveSession(sessionID, username),
    {
      ...onError('leave session'),
      onSuccess: () => console.log(`Left session`),
    },
  );
};

export const useSendMessage = (sessionID: string) => {
  const client = useQueryClient();

  return useMutation(
    (message: SendMessage) => sendMessage(sessionID, message),
    {
      ...onError('sending message'),
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
