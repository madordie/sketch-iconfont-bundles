//
//  ViewController.swift
//  MakeBundle
//
//  Created by 孙继刚 on 2017/8/18.
//  Copyright © 2017年 madordie. All rights reserved.
//

import Cocoa
import RxSwift

class ViewController: NSViewController {

    let bag = DisposeBag()
    @IBOutlet var log: NSTextView!
    var ttfs = [URL]()

    override func viewDidLoad() {
        super.viewDidLoad()

        log.isEditable = false
        Log.default.inout.asObservable()
            .filter { $0.characters.count > 0 }
            .subscribe(onNext: { [weak self] (log) in
                guard let _self = self else { return }
                _self.log.string = (_self.log.string ?? "") + log + "\n"
            })
            .addDisposableTo(bag)

        guard let ddView = view as? DDView else { return }

        ddView.draggingUrls.asObservable()
            .map({ (urls) -> [URL] in
                return urls.flatMap { $0.absoluteString.hasSuffix(".ttf") ? $0 : nil }
            })
            .filter { $0.count > 0 }
            .subscribe(onNext: { [weak self] (urls) in
                for url in urls {
                    Log.p("已提交" + url.lastPathComponent)
                }
                self?.ttfs = urls
            })
            .addDisposableTo(bag)
    }
    @IBAction func exportAction(_ sender: NSButton) {
        guard ttfs.count > 0 else {
            Log.p("未监测到有效的ttf")
            return
        }
        make(install: NSHomeDirectory() + "/Desktop/icon-bundle", ttfs: ttfs)
    }
}

extension ViewController {
    func make(install: String, ttfs: [URL]) {

        do {
            try FileManager.default.createDirectory(at: URL(fileURLWithPath: install), withIntermediateDirectories: true, attributes: nil)
        } catch {
            Log.p(error.localizedDescription)
        }

        let lib = Bundle.main.bundlePath.appending("/Contents/Resources/Lib")
        let py = lib.appending("/format.py")
        let paths = ttfs.map { $0.path }
        let status = Command.default.run(["python \(py) \(install) \(paths.joined(separator: " "))"])
        Log.p(status.output)
    }
}

