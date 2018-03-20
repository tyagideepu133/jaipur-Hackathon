import { FlaskService } from "./flask.service";
import { TestBed } from "@angular/core/testing";

describe("FlaskService", () => {

  let service: FlaskService;
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        FlaskService
      ]
    });
    service = TestBed.get(FlaskService);

  });

  it("should be able to create service instance", () => {
    expect(service).toBeDefined();
  });

});
