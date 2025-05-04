import { TestBed } from '@angular/core/testing';

import { VideoUploadServiceService } from './video-upload-service.service';

describe('VideoUploadServiceService', () => {
  let service: VideoUploadServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VideoUploadServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
