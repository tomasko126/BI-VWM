<?php

namespace App\Model;

use Nette;

class DocumentsModel {

    private $indexedArticlesFile = "../../analyzed/_indexedArticles.json";

    public function getAllStoredDocuments() {

        // Open up file with key/value pairs of docId - docName
        $file = fopen($this->indexedArticlesFile, "r");
        $result = fread($file, filesize($this->indexedArticlesFile));

        $result = json_decode($result, true);

        return $result;
    }

    public function getOneRandomDocument() {
        $allDocs = $this->getAllStoredDocuments();

        $randomDocIndex = rand(1, count((array) $allDocs));

        return $randomDocIndex;
    }

    public function getDocument($id) {
        $allDocs = $this->getAllStoredDocuments();
        $docToOpen = $allDocs[$id];

        $file = fopen("../../plain_articles/" . $docToOpen, "r");
        $result = fread($file, filesize("../../plain_articles/" . $docToOpen));

        $docObject = array();
        $docObject['id'] = $id;
        $docObject['name'] = $this->getDocumentName($id);
        $docObject['content'] = $result;

        return $docObject;
    }

    public function getSimilarDocuments($id) {
        // Run our python script in order to get similar docs
        exec("python3 ../../web_search.py " . $id, $out, $status);

        // out - [0] => path of called script, [1] => result of script
        $json = $out[1];
        $similarDocs = json_decode($json, true);

        foreach ($similarDocs['docs'] as &$doc) {
            $docId = $doc[0];
            $doc[] = $this->getDocumentName($docId);
        }

        return $similarDocs;
    }

    public function getDocumentName($id) {
        return $this->getAllStoredDocuments()[$id];
    }
}