import { TestBed } from '@angular/core/testing';

import { TextUploadServiceService } from './text-upload-service.service';

describe('TextUploadServiceService', () => {
  let service: TextUploadServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TextUploadServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
