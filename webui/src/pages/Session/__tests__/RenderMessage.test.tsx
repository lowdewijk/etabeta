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

  it("should render table markdown as a table", async () => {
    const el = await setup({message: "| a | b |\n|---|---|\n| 1 | 2 |"});
    expect(el).toContainHTML('<span data-testid="render-message"><table><thead><tr><th>a</th><th>b</th></tr></thead><tbody><tr><td>1</td><td>2</td></tr></tbody></table></span>');
  });

});