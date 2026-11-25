// Decodes QR codes in image files with macOS Vision: swift check-qr.swift a.png b.png
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let image = NSImage(contentsOfFile: path),
          let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path): cannot read"); continue
    }
    let request = VNDetectBarcodesRequest()
    request.symbologies = [.qr]
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([request])
    let values = (request.results ?? []).compactMap { $0.payloadStringValue }
    print("\((path as NSString).lastPathComponent): \(values)")
}
