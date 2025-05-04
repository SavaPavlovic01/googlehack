import { TestBed } from '@angular/core/testing';

import { YoutubeUploadServiceService } from './youtube-upload-service.service';

describe('YoutubeUploadServiceService', () => {
  let service: YoutubeUploadServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(YoutubeUploadServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
