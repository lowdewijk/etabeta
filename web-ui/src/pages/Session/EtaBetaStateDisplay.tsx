import {FC} from 'react';
import {Box} from '@mui/material';

import {EtaBetaState} from 'src/api_client/session';
import {DisplayTime} from 'src/components/DisplayTime/DisplayTime';

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
        {Object.entries(state.scores ?? {}).map(([username, score], idx) => (
          <div key={idx}>
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
      <Box>
        {state.messages
          .sort((a, b) => {
            const t = b.timestamp - a.timestamp;
            return t === 0 ? a.message.localeCompare(b.message) : t;
          })
          .map((message, midx) => (
            <Box
              key={midx}
              sx={{
                p: 1,
                m: 1,
                bgcolor: 'background.paper',
                borderRadius: 1,
                display: 'flex',
                justifyContent: 'space-around',
                alignItems: 'flex-end',
              }}
            >
              <Box>
                {message.message.split('\n').map((line, idx) => (
                  <div key={idx}>{line}</div>
                ))}
              </Box>
              <Box
                sx={{
                  whiteSpace: 'nowrap',
                  fontSize: '0.8rem',
                  paddingLeft: '1rem',
                }}
              >
                <DisplayTime timestamp={message.timestamp} />
              </Box>
            </Box>
          ))}
      </Box>
    </>
  );
};
