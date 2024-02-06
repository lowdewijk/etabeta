import {createElement, FC, Fragment, useEffect, useState} from 'react';
import * as prod from 'react/jsx-runtime';
import rehypeReact, {Options} from 'rehype-react';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import {unified} from 'unified';

export type RenderMessageProps = {
  message: string;
};

const production: Options = {
  // @ts-expect-error: the react types are missing.
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  Fragment: prod.Fragment,
  // @ts-expect-error: the react types are missing.
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  jsx: prod.jsx,
  // @ts-expect-error: the react types are missing.
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  jsxs: prod.jsxs,
  components: {
    h1: 'b',
    h2: 'b',
    h3: 'b',
  },
};

const useMarkdown = (text: string) => {
  const [Content, setContent] = useState(createElement(Fragment));

  useEffect(() => {
    const x = (async function () {
      const file = await unified()
        .use(remarkParse)
        .use(remarkRehype)
        .use(rehypeReact, production)
        .process(text);

      setContent(file.result);
    })();

    x.catch(console.error);
  }, [text]);

  return Content;
};

export const RenderMessage: FC<RenderMessageProps> = ({message}) => {
  return <span data-testid="render-message">{useMarkdown(message)}</span>;
};
