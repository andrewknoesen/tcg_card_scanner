import './App.css';
import React, { useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";

const CameraComponent = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "environment"  // Use "user" for front camera
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImgSrc(null);
  };

  return (
    <div>
      {imgSrc ? (
        <img src={imgSrc} alt="webcam" />
      ) : (
        <Webcam
          ref={webcamRef}
          audio={false}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
        />
      )}
      <div>
        {imgSrc ? (
          <button onClick={retake}>Retake</button>
        ) : (
          <button onClick={capture}>Capture</button>
        )}
      </div>
    </div>
  );
};

export default CameraComponent;

