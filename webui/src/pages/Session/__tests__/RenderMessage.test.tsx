import { render, screen } from '@testing-library/react';
import {RenderMessage, RenderMessageProps} from '../RenderMessage';

describe('RenderMessage', () => {

  const setup = async (props: RenderMessageProps) => {
    render(<RenderMessage {...props} />);
    return await screen.findByTestId('render-message');
  }

  it("should render a simple message", async () => {
    const el = await setup({message: "Hello, World!"});
    expect(el).toContainHTML("Hello, World!");
  });

  it("should render line breaks as html breaks", async () => {
    const el = await setup({message: "Hello\n\nWorld!"});
    expect(el).toContainHTML('<span data-testid="render-message"><p>Hello</p>\n<p>World!</p></span>');
  });

});