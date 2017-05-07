import { DevFolioPage } from './app.po';

describe('dev-folio App', () => {
  let page: DevFolioPage;

  beforeEach(() => {
    page = new DevFolioPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
