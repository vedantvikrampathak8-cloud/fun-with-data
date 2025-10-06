import cv2,face_recognition,numpy as np,os,sys
def load_data():
    import numpy as np,os
    if os.path.exists("faces_data.npy") and os.path.exists("names_data.npy"):
        raw_enc = list(np.load("faces_data.npy", allow_pickle=True))
        raw_names = list(np.load("names_data.npy", allow_pickle=True))
        encs = []
        names = []
        for i, e in enumerate(raw_enc):
            try:
                arr = np.asarray(e ,dtype=np.float64)
                if arr.ndim == 1 and arr.size >= 10: 
                    encs.append(arr)
                    names.append(raw_names[i] if i < len(raw_names) else f"person{i}")
            except Exception:
                continue
        # if nothing valid, return empty lists
        return encs, names
    return [], []
def save_data(enc, names):
    np.save("faces_data.npy" ,np.array(enc ,dtype=object))
    np.save("names_data.npy" ,np.array(names ,dtype=object))
known_face_encodings ,known_face_names = load_data()
cap = cv2.VideoCapture(0)
if not cap.isOpened():sys.exit("Cannot open webcam")
while True:
    ret, frame = cap.read()
    if not ret: break
    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb = small[:, :, ::-1]
    rgb = np.ascontiguousarray(rgb) 
    locs = face_recognition.face_locations(rgb)
    try:
        encs=face_recognition.face_encodings(rgb,locs)
    except Exception:
        encs=[]
    for (top,right,bottom,left), enc in zip(locs, encs):
        matches = face_recognition.compare_faces(known_face_encodings, enc) if known_face_encodings else []
        name = "Unknown"
        if matches:
            dists = face_recognition.face_distance(known_face_encodings, enc)
            idx = int(np.argmin(dists))
            if matches[idx]:
                name = known_face_names[idx]
        t,r,b,l = top*4, right*4, bottom*4, left*4
        color = (0,255,0) if name!="Unknown" else (0,0,255)
        cv2.rectangle(frame, (l,t), (r,b), color, 2)
        cv2.rectangle(frame, (l,b-30), (r,b), color, cv2.FILLED)
        cv2.putText(frame, name, (l+6,b-6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 1)
    if any(name=="Unknown" for name in [ (known_face_names[int(np.argmin(face_recognition.face_distance(known_face_encodings, e)))] if known_face_encodings else "Unknown") for e in encs ]):
        cv2.putText(frame, "Press 's' to save this face", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.imshow("Face Recognition", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    if key == ord('s') and len(encs) > 0:
        name = input("Enter name: ").strip()
        if name:
            known_face_encodings.append(encs[0])
            known_face_names.append(name)
            save_data(known_face_encodings, known_face_names)
            print("Saved", name)
cap.release()
cv2.destroyAllWindows()
