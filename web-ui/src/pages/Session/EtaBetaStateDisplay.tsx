import {FC} from 'react';
import {Box} from '@mui/material';

import {EtaBetaState} from 'src/api_client/session';

type EtaBetaStateDisplayProps = {
  state: EtaBetaState;
};

export const EtaBetaStateDisplay: FC<EtaBetaStateDisplayProps> = ({state}) => {
  if (!state) {
    return <div>No state</div>;
  }

  return (
    <>
      <div>
        <h2>Score</h2>
      </div>
      <div>
        {Object.entries(state.scores ?? {}).map(([username, score]) => (
          <div>
            {username}: {score}
          </div>
        ))}
        <br />
      </div>
      <div>
        <h2>In court</h2>
      </div>
      <div>{state.in_court || 'No one'}</div>
      <br />
      <div>
        <h2>Messages</h2>
      </div>
      <div>
        {state.messages
          .sort((a, b) => {
            const t = b.timestamp - a.timestamp;
            return t === 0 ? a.message.localeCompare(b.message) : t;
          })
          .map((message, idx) => (
            <Box
              key={idx}
              sx={{p: 1, m: 1, bgcolor: 'background.paper', borderRadius: 1}}
            >
              {message.message}
            </Box>
          ))}
      </div>
    </>
  );
};
