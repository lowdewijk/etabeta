import {FC} from 'react';
import {Box, List, ListItem} from '@mui/material';

import {EtaBetaArgument, EtaBetaState} from 'src/api_client/session';
import {DisplayTime} from 'src/components/DisplayTime/DisplayTime';

type EtaBetaStateDisplayProps = {
  state: EtaBetaState;
};

export const EtaBetaStateDisplay: FC<EtaBetaStateDisplayProps> = ({state}) => {
  if (!state) {
    return <div>No state</div>;
  }

  const renderArg = (arg: EtaBetaArgument, idx: number) => {
    return (
      <ListItem key={idx} sx={{pl: 1, pb: 0, pt: 0.5}}>
        {arg.argument}
        {arg.counter_arguments.length > 0 && (
          <List
            sx={{
              listStyleType: 'disc',
              pl: 1,
              pt: 0,
              pb: 0,
              m: 0,
              '& .MuiListItem-root': {
                display: 'list-item',
              },
            }}
          >
            {arg.counter_arguments.map((child, aidx) => renderArg(child, aidx))}
          </List>
        )}
      </ListItem>
    );
  };

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
      <div
        style={{
          paddingTop: '1rem',
        }}
      >
        <h2>Summary</h2>
      </div>
      <div>
        <List
          sx={{
            listStyleType: 'disc',
            pl: 2,
            pb: 0,
            m: 0,
            '& .MuiListItem-root': {
              display: 'list-item',
            },
          }}
        >
          {state.summary.map((arg, aidx) => renderArg(arg, aidx))}
        </List>
      </div>
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
