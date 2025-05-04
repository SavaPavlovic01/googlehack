import { TestBed } from '@angular/core/testing';

import { TwitterUploadServiceService } from './twitter-upload-service.service';

describe('TwitterUploadServiceService', () => {
  let service: TwitterUploadServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TwitterUploadServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
